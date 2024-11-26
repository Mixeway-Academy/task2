package com.example.thymeleaf.util;

import java.time.LocalDate;

public class LogMaskingUtil {
    
    // Replace birthdate with masked format
    public static String maskBirthday(LocalDate birthday) {
        if (birthday == null) return "****-**-**";
        return "****-**-**";
    }

    // Generic method to mask any field with '***'
    public static String maskField(String value) {
        if (value == null || value.isEmpty()) return value;
        return "***";
    }
}

