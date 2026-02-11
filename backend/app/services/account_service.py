from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.account_request import AccountRequest
from app.schemas.account import AccountCreate
from app.schemas.transaction import TransactionCreate
import uuid

class AccountService:
    @staticmethod
    def create_account(db: Session, user_id: int, payload):
        acc_number = f"ACC{str(uuid.uuid4())[:12].upper()}"
        # allow creating active accounts (admin) or typical accounts with zero balance
        balance = Decimal(str(getattr(payload, 'initial_deposit', 0) or 0))
        status = getattr(payload, 'status', 'ACTIVE')
        branch = getattr(payload, 'branch', None)
        # simple IFSC generator
        ifsc = f"IFSC{str(uuid.uuid4())[:7].upper()}"
        new = Account(user_id=user_id, account_number=acc_number, account_type=payload.account_type, balance=balance, status=status, branch=branch, ifsc=ifsc)
        db.add(new)
        db.commit()
        db.refresh(new)
        return new

    @staticmethod
    def create_account_request(db: Session, user_id: int, payload: AccountCreate):
        # check duplicate pending
        existing = db.query(AccountRequest).filter(AccountRequest.user_id == user_id, AccountRequest.status == 'PENDING_APPROVAL').first()
        if existing:
            raise Exception('There is already a pending account request')
        req = AccountRequest(user_id=user_id, account_type=payload.account_type, branch=getattr(payload, 'branch', None), initial_deposit=Decimal(str(getattr(payload, 'initial_deposit', 0) or 0)))
        db.add(req)
        db.commit()
        db.refresh(req)
        return req

    @staticmethod
    def get_pending_requests(db: Session):
        return db.query(AccountRequest).filter(AccountRequest.status == 'PENDING_APPROVAL').all()

    @staticmethod
    def get_request(db: Session, request_id: int):
        return db.get(AccountRequest, request_id)

    @staticmethod
    def approve_request(db: Session, request_id: int, admin_user_id: int):
        req = db.get(AccountRequest, request_id)
        if not req:
            raise Exception('Request not found')
        if getattr(req, 'status', None) != 'PENDING_APPROVAL':
            raise Exception('Request is not pending')
        # create account with initial deposit
        from types import SimpleNamespace
        payload = SimpleNamespace(account_type=getattr(req,'account_type',None), initial_deposit=float(getattr(req,'initial_deposit',0) or 0), branch=getattr(req,'branch',None))
        acc = AccountService.create_account(db, int(getattr(req,'user_id')), payload)
        # if initial deposit > 0 create transaction
        if Decimal(str(getattr(req,'initial_deposit',0))) > Decimal('0'):
            tx = Transaction(from_account=None, to_account=acc.account_number, amount=Decimal(str(getattr(req,'initial_deposit',0))), transaction_type='CREDIT', status='COMPLETED')
            db.add(tx)
        req.status = 'ACTIVE'
        db.add(req)
        db.commit()
        db.refresh(acc)
        return acc

    @staticmethod
    def reject_request(db: Session, request_id: int, reason: str, admin_user_id: int):
        req = db.get(AccountRequest, request_id)
        if not req:
            raise Exception('Request not found')
        if getattr(req, 'status', None) != 'PENDING_APPROVAL':
            raise Exception('Request is not pending')
        req.status = 'REJECTED'
        req.reason = reason
        db.add(req)
        db.commit()
        return req

    @staticmethod
    def admin_create_account(db: Session, user_id: int, payload: dict):
        # payload is expected to have account_type, initial_deposit, branch
        from types import SimpleNamespace
        p = SimpleNamespace(**payload)
        return AccountService.create_account(db, user_id, p)

    @staticmethod
    def get_user_accounts(db: Session, user_id: int):
        return db.query(Account).filter(Account.user_id == user_id).all()

    @staticmethod
    def get_account(db: Session, account_id: int):
        return db.get(Account, account_id)

    @staticmethod
    def get_account_by_number(db: Session, account_number: str):
        return db.query(Account).filter(Account.account_number == account_number).first()

    @staticmethod
    def deposit(db: Session, from_user_id: int, to_account_number: str, amount: Decimal):
        acc = db.query(Account).filter(Account.account_number == to_account_number).first()
        if not acc:
            raise Exception('Account not found')
        if acc.status != 'ACTIVE':  # type: ignore
            raise Exception('Account is inactive')
        amount = Decimal(str(amount))
        if amount <= 0:
            raise Exception('Amount must be positive')
        
        try:
            acc.balance = Decimal(str(acc.balance)) + amount  # type: ignore
            tx = Transaction(
                from_account=None, 
                to_account=to_account_number, 
                amount=amount, 
                transaction_type='CREDIT',
                status='COMPLETED'
            )
            db.add(tx)
            db.add(acc)
            db.commit()
            return {"msg": "Deposit successful", "transaction_id": tx.id}
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def withdraw(db: Session, from_user_id: int, from_account_number: str, amount: Decimal):
        acc = db.query(Account).filter(Account.account_number == from_account_number).first()
        if not acc:
            raise Exception('Account not found')
        if acc.status != 'ACTIVE':  # type: ignore
            raise Exception('Account is inactive')
        if acc.user_id != from_user_id:  # type: ignore
            raise Exception('Unauthorized')
        
        amount = Decimal(str(amount))
        if amount <= 0:
            raise Exception('Amount must be positive')
        if Decimal(str(acc.balance)) < amount:
            raise Exception('Insufficient funds')
        
        try:
            acc.balance = Decimal(str(acc.balance)) - amount  # type: ignore
            tx = Transaction(
                from_account=from_account_number, 
                to_account=None, 
                amount=amount, 
                transaction_type='DEBIT',
                status='COMPLETED'
            )
            db.add(tx)
            db.add(acc)
            db.commit()
            return {"msg": "Withdrawal successful", "transaction_id": tx.id}
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def transfer(db: Session, from_user_id: int, from_account_number: str, to_account_number: str, amount: Decimal, idempotency_key: Optional[str] = None):
        amount = Decimal(str(amount))
        if amount <= 0:
            raise Exception('Amount must be positive')
        
        # Check for duplicate transfer (idempotency)
        if idempotency_key:
            existing = db.query(Transaction).filter(
                Transaction.from_account == from_account_number,
                Transaction.to_account == to_account_number,
                Transaction.amount == amount,
                Transaction.transaction_type == 'TRANSFER'
            ).order_by(Transaction.created_at.desc()).first()
            if existing:
                return {"msg": "Transfer already processed", "transaction_id": existing.id}
        
        try:
            # Use transaction for atomicity
            from_acc = db.query(Account).filter(Account.account_number == from_account_number).with_for_update().first()
            to_acc = db.query(Account).filter(Account.account_number == to_account_number).with_for_update().first()
            
            if not from_acc or not to_acc:
                raise Exception('Account not found')
            if from_acc.status != 'ACTIVE' or to_acc.status != 'ACTIVE':  # type: ignore
                raise Exception('One or both accounts are inactive')
            if from_acc.user_id != from_user_id:  # type: ignore
                raise Exception('Unauthorized')
            if Decimal(str(from_acc.balance)) < amount:
                raise Exception('Insufficient funds')
            
            from_acc.balance = Decimal(str(from_acc.balance)) - amount  # type: ignore
            to_acc.balance = Decimal(str(to_acc.balance)) + amount  # type: ignore
            tx = Transaction(
                from_account=from_account_number, 
                to_account=to_account_number, 
                amount=amount, 
                transaction_type='TRANSFER',
                status='COMPLETED'
            )
            db.add(from_acc)
            db.add(to_acc)
            db.add(tx)
            db.commit()
            return {"msg": "Transfer successful", "transaction_id": tx.id}
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def get_history(db: Session, user_id: int, limit: int = 50):
        user_accounts = db.query(Account.account_number).filter(Account.user_id == user_id).all()
        account_numbers = [a[0] for a in user_accounts]
        if not account_numbers:
            return []
        return db.query(Transaction).filter(
            (Transaction.from_account.in_(account_numbers)) | (Transaction.to_account.in_(account_numbers))
        ).order_by(Transaction.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_dashboard_summary(db: Session, user_id: int):
        accounts = db.query(Account).filter(Account.user_id == user_id).all()
        total_balance = sum(Decimal(str(a.balance)) for a in accounts)  # type: ignore
        account_count = len(accounts)
        
        if accounts:
            account_numbers = [a.account_number for a in accounts]
            recent_txns = db.query(Transaction).filter(
                (Transaction.from_account.in_(account_numbers)) | (Transaction.to_account.in_(account_numbers))
            ).order_by(Transaction.created_at.desc()).limit(5).all()
        else:
            recent_txns = []
        
        return {
            "total_balance": float(total_balance),
            "account_count": account_count,
            "recent_transactions": len(recent_txns),
            "accounts": [{"id": a.id, "account_number": a.account_number, "balance": float(a.balance), "type": a.account_type} for a in accounts]  # type: ignore
        }

