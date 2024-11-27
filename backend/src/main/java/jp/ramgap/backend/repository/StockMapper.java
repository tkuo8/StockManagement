package jp.ramgap.backend.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import jp.ramgap.backend.domain.stock.model.Stock;

@Mapper
public interface StockMapper {
    /** 株情報登録 */
    public int insertOne(Stock stock);

    // ユーザーの保有株情報全体を取得
    public List<Stock> findStocksByUserId(int userId);
}
