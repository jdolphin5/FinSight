package com.jd.finsight.util;

import jakarta.servlet.http.HttpServletRequest;

public class ControllerUtil {
    public static String getClientIp(HttpServletRequest request) {
        String ip = request.getHeader("X-Forwarded-For"); // Handle proxies
        if (ip == null || ip.isEmpty() || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getRemoteAddr(); // Fallback to remote address if no proxy is involved
        }

        // If multiple IPs are returned in X-Forwarded-For, take the first one
        if (ip != null && ip.contains(",")) {
            ip = ip.split(",")[0].trim();
        }

        // Ensure the IP address is in IPv4 format (skip IPv6 addresses)
        if (isValidIPv4(ip)) {
            return ip;
        } else {
            return "No valid IPv4 address found";
        }
    }

    // Utility method to validate if the IP address is IPv4
    private static boolean isValidIPv4(String ip) {
        String ipv4Pattern = "^([0-9]{1,3}\\.){3}[0-9]{1,3}$";
        return ip.matches(ipv4Pattern);
    }
}
