package jp.ramgap.backend.model;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class StockInfoEnteredByUser {
    private Integer ticker;
    private Integer stockPrices;
    private Integer stockNumberHeld;
    private Integer goalPrices;
}
