/**
 * Spring Data repositories for the shared schema. One database today because
 * this is a modular monolith. Do not treat a repository as the place to hide
 * money rules — those stay on {@code Money} and {@code Payment}.
 */
package com.baypay.shared.persistence;
