package jp.ramgap.backend.repository;

import org.apache.ibatis.annotations.Mapper;

import jp.ramgap.backend.domain.stock.model.Stock;

@Mapper
public interface StockMapper {
    /** 株情報登録 */
    public int insertOne(Stock stock);

}
