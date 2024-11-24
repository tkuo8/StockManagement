package jp.ramgap.backend.form;

import java.math.BigDecimal;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class StocksAddForm {
    private String symbol;
    private BigDecimal purchasePrice;
    private Integer quantity;
    private BigDecimal targetPrice;
    private BigDecimal cutLossPrice;
}
