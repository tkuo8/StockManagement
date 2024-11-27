package jp.ramgap.backend.domain.stock.service;

import java.util.List;

import jp.ramgap.backend.domain.stock.model.Stock;

public interface StockService {

    // 株情報の登録（１件）
    public void addStock(Stock stock);

    // ユーザの株情報全体の取得
    public List<Stock> getStocksByUserId(int userId);
}
