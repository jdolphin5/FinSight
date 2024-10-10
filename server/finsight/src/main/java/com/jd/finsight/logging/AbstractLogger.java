package com.jd.finsight.logging;

public abstract class AbstractLogger {
    protected LogFactory logFactory;

    public AbstractLogger(LogFactory logFactory) {
        this.logFactory = logFactory;
    }

    public abstract void writeLogsToFile(String log);
}
