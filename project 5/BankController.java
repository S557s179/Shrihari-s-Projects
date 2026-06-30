package com.bank.api;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/bank")
public class BankController {

    private final BankService bankService;

    public BankController(BankService bankService) {
        this.bankService = bankService;
    }

    @PostMapping("/account")
    public Account createAccount(@RequestBody CreateAccountRequest request) {
        return bankService.createAccount(request);
    }

    @PostMapping("/transfer")
    public Transaction transfer(@RequestBody TransferRequest request) {
        return bankService.transfer(request);
    }
}
