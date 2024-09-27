package com.jd.finsight.services;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import com.jd.finsight.domain.HistoricalStockDataEntity;

public interface HistoricalStockDataService {
    HistoricalStockDataEntity createStock(HistoricalStockDataEntity historicalStockData);

    List<HistoricalStockDataEntity> findAll();

    Optional<HistoricalStockDataEntity> findOne(Long id);

    List<HistoricalStockDataEntity> findAllWithCode(String code);

    List<HistoricalStockDataEntity> findAllWithCodeAndDateBetween(String code, LocalDateTime dateFromDateTime,
            LocalDateTime dateToDateTime);

    Optional<HistoricalStockDataEntity> deleteStock(Long id);
}
