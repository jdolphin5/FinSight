package com.jd.finsight.logging.impl;

import com.jd.finsight.logging.AbstractLogger;
import com.jd.finsight.logging.LogFactory;

public class CommandLogger extends AbstractLogger {

    public CommandLogger(LogFactory logFactory) {
        super(logFactory);
    }

    @Override
    public void writeLogsToFile(String log) {
        logFactory.writeLogsToFile(log);
    }

}
