package com.example.thymeleaf.util;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public final class LogMasker {

    private static final String MASK = "***";

    public static String masked(Object value) {
        return value == null ? null : MASK;
    }
}
