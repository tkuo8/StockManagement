package jp.ramgap.backend.domain.stock.model;

import java.math.BigDecimal;
import java.time.LocalDateTime;

import lombok.Data;

@Data
public class Stock {
    private Integer stockId;
    private Integer userId;
    private String symbol;
    private BigDecimal purchasePrice;
    private Integer quantity;
    private BigDecimal targetPrice;
    private BigDecimal cutlossPrice;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
