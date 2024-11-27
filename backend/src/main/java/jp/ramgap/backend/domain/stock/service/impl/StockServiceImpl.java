package jp.ramgap.backend.domain.stock.service.impl;

import org.springframework.stereotype.Service;

import jp.ramgap.backend.domain.stock.model.Stock;
import jp.ramgap.backend.domain.stock.service.StockService;
import jp.ramgap.backend.repository.StockMapper;

@Service
public class StockServiceImpl implements StockService {

    private final StockMapper stockMapper;

    public StockServiceImpl(StockMapper stockMapper) {
        this.stockMapper = stockMapper;
    }

    // 株情報登録（１件）
    @Override
    public void addStock(Stock stock) {
        stockMapper.insertOne(stock);
    }
}
