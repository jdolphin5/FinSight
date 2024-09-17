package com.jd.finsight.mappers.impl;

import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Component;

import com.jd.finsight.domain.HistoricalStockDataEntity;
import com.jd.finsight.domain.dto.HistoricalStockDataDto;
import com.jd.finsight.mappers.Mapper;

@Component
public class HistoricalStockDataMapperImpl implements Mapper<HistoricalStockDataEntity, HistoricalStockDataDto> {
    private ModelMapper modelMapper;

    public HistoricalStockDataMapperImpl(ModelMapper modelMapper) {
        this.modelMapper = modelMapper;
    }

    @Override
    public HistoricalStockDataDto mapTo(HistoricalStockDataEntity historicalStockDataEntity) {
        return modelMapper.map(historicalStockDataEntity, HistoricalStockDataDto.class);
    }

    @Override
    public HistoricalStockDataEntity mapFrom(HistoricalStockDataDto historicalStockDataDto) {
        return modelMapper.map(historicalStockDataDto, HistoricalStockDataEntity.class);
    }
}
