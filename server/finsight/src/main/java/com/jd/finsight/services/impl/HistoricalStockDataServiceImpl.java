package com.jd.finsight.services.impl;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

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

    @Override
    public List<HistoricalStockDataEntity> findAll() {
        return StreamSupport.stream(historicalStockDataRepository.findAll().spliterator(), false)
                .collect(Collectors.toList());
    }

    @Override
    public Optional<HistoricalStockDataEntity> findOne(Long id) {
        return historicalStockDataRepository.findById(id);
    }

}
