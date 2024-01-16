package com.example.thymeleaf.entity;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Getter
@Setter
@Entity
@Table(name = "address")
@EqualsAndHashCode(of = {"id"})
public class Address {
    @Transient
    private static final Logger logger = LoggerFactory.getLogger(Address.class);

    @Id
    private String id;

    @Column(name = "zip_code")
    private String zipCode;

    private String street;
    private String number;
    private String complement;
    private String district;
    private String city;
    private String state;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @OneToOne
    @JoinColumn(name = "fk_student")
    private Student student;

    @PrePersist
    private void prePersist() {
        this.id = UUID.randomUUID().toString();
        this.createdAt = LocalDateTime.now();
    }

    @PreUpdate
    private void preUpdate() {
        this.updatedAt = LocalDateTime.now();
    }

    @Override
    public String toString() {
        // Zastąpienie wartości na '*'
        String id_hidden = "*".repeat(id.length());
        String zipCode_hidden = "*".repeat(zipCode.length());
        String street_hidden = "*".repeat(street.length());
        String number_hidden = "*".repeat(number.length());
        String complement_hidden = "*".repeat(complement.length());
        String district_hidden = "*".repeat(district.length());
        String city_hidden = "*".repeat(city.length());
        String state_hidden = "*".repeat(state.length());

        return "Address{" +
                "id='" + id_hidden + '\'' +
                ", zipCode='" + zipCode_hidden + '\'' +
                ", street='" + street_hidden + '\'' +
                ", number='" + number_hidden + '\'' +
                ", complement='" + complement_hidden + '\'' +
                ", district='" + district_hidden + '\'' +
                ", city='" + city_hidden + '\'' +
                ", state='" + state_hidden + '\'' +
                ", createdAt=" + createdAt +
                ", updatedAt=" + updatedAt +
                '}';
    }
}
