package com.jd.finsight.controllers;

import java.sql.Timestamp;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.jd.finsight.domain.dto.HistoricalStockDataDto;
import com.jd.finsight.mappers.Mapper;
import com.jd.finsight.services.HistoricalStockDataService;
import com.jd.finsight.domain.HistoricalStockDataEntity;

import lombok.extern.java.Log;

import com.jd.finsight.util.StockUtil;

@RestController
@Log
public class StockController {

    private HistoricalStockDataService historicalStockDataService;

    private Mapper<HistoricalStockDataEntity, HistoricalStockDataDto> historicalStockDataMapper;

    public StockController(HistoricalStockDataService historicalStockDataService,
            Mapper<HistoricalStockDataEntity, HistoricalStockDataDto> historicalStockDataMapper) {
        this.historicalStockDataService = historicalStockDataService;
        this.historicalStockDataMapper = historicalStockDataMapper;
    }

    @GetMapping(path = "/stocks")
    public HistoricalStockDataDto retreieveStock() {
        return HistoricalStockDataDto.builder()
                .id(1L)
                .code("AMZN")
                .local_time(Timestamp.valueOf(StockUtil.convertRawTimestamp("02.09.2024 00:00:00.000")))
                .open(228.957)
                .low(228.957)
                .high(228.957)
                .close(228.957)
                .volume(1.0)
                .build();
    }

    @PostMapping(path = "/stocks")
    public HistoricalStockDataDto createStock(@RequestBody final HistoricalStockDataDto stock) {
        HistoricalStockDataEntity historicalStockDataEntity = historicalStockDataMapper.mapFrom(stock);
        HistoricalStockDataEntity savedHistoricalStockDataEntity = historicalStockDataService
                .createStock(historicalStockDataEntity);

        log.info("Retrieved stock: " + savedHistoricalStockDataEntity.toString());

        return historicalStockDataMapper.mapTo(savedHistoricalStockDataEntity);
    }

}
