package jp.ramgap.backend.domain.stock.service;

import jp.ramgap.backend.domain.stock.model.Stock;

public interface StockService {

    // 株情報の登録（１件）
    public void addStock(Stock stock);
}
