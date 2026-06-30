package com.bank.api;

import lombok.Data;
import java.math.BigDecimal;

@Data
public class CreateAccountRequest {
    private String ownerName;
    private BigDecimal initialDeposit;
}
