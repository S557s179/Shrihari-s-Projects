package com.bank.api;

import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;

@Service
public class BankService {

    private final AccountRepository accountRepo;
    private final TransactionRepository transactionRepo;

    public BankService(AccountRepository accountRepo, TransactionRepository transactionRepo) {
        this.accountRepo = accountRepo;
        this.transactionRepo = transactionRepo;
    }

    public Account createAccount(CreateAccountRequest request) {
        Account acc = new Account();
        acc.setOwnerName(request.getOwnerName());
        acc.setAccountNumber(UUID.randomUUID().toString());
        acc.setBalance(request.getInitialDeposit());
        return accountRepo.save(acc);
    }

    public Transaction transfer(TransferRequest request) {

        Account from = accountRepo.findByAccountNumber(request.getFromAccount())
                .orElseThrow(() -> new ResourceNotFoundException("From account not found"));

        Account to = accountRepo.findByAccountNumber(request.getToAccount())
                .orElseThrow(() -> new ResourceNotFoundException("To account not found"));

        if (from.getBalance().compareTo(request.getAmount()) < 0) {
            throw new InsufficientFundsException("Insufficient balance");
        }

        from.setBalance(from.getBalance().subtract(request.getAmount()));
        to.setBalance(to.getBalance().add(request.getAmount()));

        accountRepo.save(from);
        accountRepo.save(to);

        Transaction tx = new Transaction();
        tx.setFromAccount(from.getAccountNumber());
        tx.setToAccount(to.getAccountNumber());
        tx.setAmount(request.getAmount());
        tx.setTimestamp(LocalDateTime.now());
        tx.setType("TRANSFER");

        return transactionRepo.save(tx);
    }
}
