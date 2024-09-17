package com.jd.finsight.repositories;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.jd.finsight.domain.HistoricalStockDataEntity;

@Repository
public interface HistoricalStockDataRepository extends CrudRepository<HistoricalStockDataEntity, Long> {
}