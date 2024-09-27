package com.jd.finsight.services.impl;

import java.util.List;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

import org.springframework.stereotype.Service;

import com.jd.finsight.domain.HistoricalStockDataEntity;
import com.jd.finsight.repositories.HistoricalStockDataRepository;
import com.jd.finsight.services.HistoricalStockDataService;
import com.jd.finsight.util.StockUtil;

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

    @Override
    public List<HistoricalStockDataEntity> findAll() {
        return StreamSupport.stream(historicalStockDataRepository.findAll().spliterator(), false)
                .collect(Collectors.toList());
    }

    @Override
    public Optional<HistoricalStockDataEntity> findOne(Long id) {
        return historicalStockDataRepository.findById(id);
    }

    @Override
    public List<HistoricalStockDataEntity> findAllWithCode(String code) {
        List<HistoricalStockDataEntity> historicalStockDataEntityList = StreamSupport
                .stream(historicalStockDataRepository.findAll().spliterator(), false)
                .collect(Collectors.toList());

        return StockUtil.filterByCode(historicalStockDataEntityList, code);
    }

    @Override
    public List<HistoricalStockDataEntity> findAllWithCodeAndDateBetween(String code, LocalDateTime dateFromDateTime,
            LocalDateTime dateToDateTime) {
        List<HistoricalStockDataEntity> historicalStockDataEntityList = StreamSupport
                .stream(historicalStockDataRepository.findAll().spliterator(), false)
                .collect(Collectors.toList());

        List<HistoricalStockDataEntity> historicalStockDataEntityWithCodeAndDateBetweenList = StockUtil
                .filterByDate(StockUtil.filterByCode(historicalStockDataEntityList, code), dateFromDateTime,
                        dateToDateTime);
        return historicalStockDataEntityWithCodeAndDateBetweenList;
    }

}
