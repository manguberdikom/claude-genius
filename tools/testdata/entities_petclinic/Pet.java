/*
 * Manba: https://github.com/spring-projects/spring-petclinic, commit 500158f,
 * src/main/java/org/springframework/samples/petclinic/owner/Pet.java.
 * Qisqartirilgan: maydonlar va annotatsiyalar qoldi, metodlar olib tashlandi.
 * Sinov: @OneToMany + @JoinColumn(name = "pet_id") FK ni visits jadvaliga
 * beradi (schema.sql: visits.pet_id).
 *
 * Copyright 2012-2025 the original author or authors.
 * Licensed under the Apache License, Version 2.0:
 * https://www.apache.org/licenses/LICENSE-2.0
 */
package org.springframework.samples.petclinic.owner;

import java.time.LocalDate;
import java.util.LinkedHashSet;
import java.util.Set;

import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.samples.petclinic.model.NamedEntity;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.OrderBy;
import jakarta.persistence.Table;

@Entity
@Table(name = "pets")
public class Pet extends NamedEntity {

	@Column
	@DateTimeFormat(pattern = "yyyy-MM-dd")
	private LocalDate birthDate;

	@ManyToOne
	@JoinColumn(name = "type_id")
	private PetType type;

	@OneToMany(cascade = CascadeType.ALL, fetch = FetchType.EAGER)
	@JoinColumn(name = "pet_id")
	@OrderBy("date ASC")
	private final Set<Visit> visits = new LinkedHashSet<>();

}
