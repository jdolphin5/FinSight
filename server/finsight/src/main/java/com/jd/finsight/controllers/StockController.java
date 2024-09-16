package com.jd.finsight.controllers;

import java.sql.Timestamp;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.jd.finsight.domain.Stock;

import lombok.extern.java.Log;

import com.jd.finsight.util.StockUtil;

@RestController
@Log
public class StockController {

    @GetMapping(path = "/stocks")
    public Stock retreieveStock() {
        return Stock.builder()
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
    public Stock createStock(@RequestBody final Stock stock) {
        log.info("Retrieved stock: " + stock.toString());
        return stock;
    }

}
