package jp.ramgap.backend.model;

import java.math.BigDecimal;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class StockRegisteredByUser {
    private String symbol;
    private BigDecimal purchasePrice;
    private Integer quantity;
    private BigDecimal targetPrice;
    private BigDecimal cutlossPrice;
}
