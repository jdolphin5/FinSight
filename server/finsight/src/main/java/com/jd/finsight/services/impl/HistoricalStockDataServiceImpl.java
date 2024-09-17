package com.jd.finsight.services.impl;

import org.springframework.stereotype.Service;

import com.jd.finsight.domain.HistoricalStockDataEntity;
import com.jd.finsight.repositories.HistoricalStockDataRepository;
import com.jd.finsight.services.HistoricalStockDataService;

@Service
public class HistoricalStockDataServiceImpl implements HistoricalStockDataService {
    private HistoricalStockDataRepository historicalStockDataRepository;

    public HistoricalStockDataServiceImpl(HistoricalStockDataRepository historicalStockDataRepository) {
        this.historicalStockDataRepository = historicalStockDataRepository;
    }

    @Override
    public HistoricalStockDataEntity createStock(HistoricalStockDataEntity historicalStockDataEntity) {
        return historicalStockDataRepository.save(historicalStockDataEntity);
    }
}
