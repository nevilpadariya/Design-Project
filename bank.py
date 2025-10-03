from banking_system import BankingSystem

class BankingSystemImpl(BankingSystem):
    def __init__(self):
        self.accounts = {}
        self.transactions = {}
        self.scheduled_transfers = {}
        self.transfer_counter = 1
    
    def _process_expired_transfers(self, timestamp):
        for transfer_id, transfer in list(self.scheduled_transfers.items()):
            if transfer["status"] == "PENDING":
                # Transfer expires at the beginning of the next millisecond after 24 hours
                expiration_time = transfer["timestamp"] + 86400000 + 1
                if timestamp >= expiration_time:
                    transfer["status"] = "EXPIRED"
                    self.accounts[transfer["source"]] += transfer["amount"]
    
    def create_account(self, timestamp, account_id):
        self._process_expired_transfers(timestamp)
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = 0
        self.transactions[account_id] = 0
        return True
    
    def deposit(self, timestamp, account_id, amount):
        self._process_expired_transfers(timestamp)
        if account_id not in self.accounts:
            return None
        self.accounts[account_id] += amount
        self.transactions[account_id] += amount
        return self.accounts[account_id]
    
    def pay(self, timestamp, account_id, amount):
        self._process_expired_transfers(timestamp)
        if account_id not in self.accounts:
            return None
        if self.accounts[account_id] < amount:
            return None
        self.accounts[account_id] -= amount
        self.transactions[account_id] += amount
        return self.accounts[account_id]
    
    def top_activity(self, timestamp, n):
        self._process_expired_transfers(timestamp)
        sorted_accounts = sorted(
            self.transactions.items(), key=lambda item: (-item[1], item[0])
        )
        
        result = []
        for i in range(min(n, len(sorted_accounts))):
            account_id, value = sorted_accounts[i]
            result.append(f"{account_id}({value})")
            
        return result
    
    def transfer(self, timestamp, source_account_id, target_account_id, amount):
        self._process_expired_transfers(timestamp)
        
        # Check if source and target are the same
        if source_account_id == target_account_id:
            return None
            
        # Check if accounts exist
        if source_account_id not in self.accounts or target_account_id not in self.accounts:
            return None
            
        # Check if source has sufficient funds
        if self.accounts[source_account_id] < amount:
            return None
        
        # Withdraw money from source account
        self.accounts[source_account_id] -= amount
        
        # Create scheduled transfer
        transfer_id = f"transfer{self.transfer_counter}"
        self.scheduled_transfers[transfer_id] = {
            "source": source_account_id,
            "target": target_account_id,
            "amount": amount,
            "timestamp": timestamp,
            "status": "PENDING"
        }
        self.transfer_counter += 1
        
        return transfer_id
    
    def accept_transfer(self, timestamp, account_id, transfer_id):
        self._process_expired_transfers(timestamp)
        
        # Check if transfer exists
        if transfer_id not in self.scheduled_transfers:
            return False
        
        transfer = self.scheduled_transfers[transfer_id]
        
        # Check if the account_id is the target account
        if transfer["target"] != account_id:
            return False
            
        # Check if transfer is still pending (not expired or already accepted)
        if transfer["status"] != "PENDING":
            return False
        
        # Check if transfer has expired
        expiration_time = transfer["timestamp"] + 86400000
        if timestamp >= expiration_time:
            # Mark as expired and refund source account
            transfer["status"] = "EXPIRED"
            self.accounts[transfer["source"]] += transfer["amount"]
            return False
            
        # Accept the transfer
        self.accounts[transfer["target"]] += transfer["amount"]
        self.transactions[transfer["source"]] += transfer["amount"]
        self.transactions[transfer["target"]] += transfer["amount"]
        transfer["status"] = "ACCEPTED"
        
        return True