package com.jd.finsight.logging;

public abstract class LogFactory {
    protected String log;
    protected String filePath;

    public LogFactory(String filePath) {
        this.filePath = filePath;
    }

    public abstract void writeLogsToFile(String log);
}
