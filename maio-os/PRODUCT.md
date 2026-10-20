# Maio OS

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Ricardo uses Maio OS to inspect household projects, agents, documents, and the local machine.

## Product Purpose

A single workspace with defined sections. Ricardo explicitly requested replacing the floating desktop: content opens in the main page, with persistent navigation and no floating windows or pop-up search.

## Operating Context

The static build reads the generated `MAIO_DATA` snapshot. The local companion adds machine readings, the fleet board, document reading, vault search, and existing gated actions. Snapshot and live data must remain distinguishable.

## Capabilities and Constraints

- Work contains Projects, Kanban, and Agents. Knowledge contains Library, PRDs, and Vault. System contains Machine, Stack, and About. Overview and Search provide entry points.
- Project, agent, and document details stay inside their section, with parent breadcrumbs and bookmarkable routes. Back and Forward follow ordinary browser history.
- The data normalizers, read-only vault boundary, and existing backend action confirmations remain in force. Beast is the only vault writer.
- Existing `#desk`, project, agent, report, and file links remain supported. Legacy window geometry is ignored without modifying its saved storage.

## Brand Commitments

Keep the Maio OS name and existing local logo, icon sprite, and agent portraits. The section redesign retains the established light interface and system font stacks.

## Product Principles

- Give each kind of work a stable, visible home.
- Keep navigation available while content scrolls, including on phones.
- Open a named document directly when its format is supported; make unavailable local content explicit.
- Preserve real content and describe data freshness accurately.
