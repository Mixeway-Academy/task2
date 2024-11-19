package com.example.thymeleaf.entity;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

import lombok.ToString;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Getter
@Setter
@Entity
@Table(name = "address")
@ToString
@EqualsAndHashCode(of = {"id"})
public class Address {
    @Transient
    private static final Logger logger = LoggerFactory.getLogger(Address.class);

    @Id
    private String id;
    @ToString.Exclude
    @Column(name = "zip_code")
    private String zipCode;
    @ToString.Exclude
    private String street;
    @ToString.Exclude
    private String number;
    @ToString.Exclude
    private String complement;
    @ToString.Exclude
    private String district;
    @ToString.Exclude
    private String city;
    @ToString.Exclude
    private String state;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    @ToString.Exclude
    @OneToOne
    @JoinColumn(name = "fk_student")
    private Student student;

    @PrePersist
    private void prePersist() {
        this.id = UUID.randomUUID().toString();
        this.createdAt = LocalDateTime.now();
    }
    @ToString.Include(name = "zipCode")
    private String maskZipCode() {
        return "******";
    }
    @ToString.Include(name = "street")
    private String maskPassword() {
        return "******";
    }
    @ToString.Include(name = "number")
    private String maskNumber() {
        return "******";
    }
    @ToString.Include(name = "complement")
    private String maskComplement() {
        return "******";
    }
    @ToString.Include(name = "district")
    private String maskDistrict() {
        return "******";
    }
    @ToString.Include(name = "city")
    private String maskCity() {
        return "******";
    }
    @ToString.Include(name = "state")
    private String maskState() {
        return "******";
    }
    @PreUpdate
    private void preUpdate() {
        this.updatedAt = LocalDateTime.now();
    }

}
