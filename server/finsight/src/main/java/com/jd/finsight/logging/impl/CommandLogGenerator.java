package com.jd.finsight.logging.impl;

import com.jd.finsight.logging.LogGenerator;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import com.jd.finsight.logging.LogFactory;

@Component
public class CommandLogGenerator extends LogGenerator {

    public CommandLogGenerator(@Value("${log.file:logs/CommandLogs.txt}") String filePath) {
        super(filePath);
    }

    @Override
    public void createLogger() {
        LogFactory genericLogFactory = new GenericLogFactory(filePath);
        this.abstractLogger = new CommandLogger(genericLogFactory);
    }

}
