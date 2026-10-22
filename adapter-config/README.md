# adapter-config: connecting an ONIX adapter to a Sygnal network

This folder holds settings that connect a participant's [Beckn ONIX](https://github.com/beckn/beckn-onix) adapter to a Sygnal network's telemetry. The network's coordination and operations dashboards can then show the adapter's traffic. The setup uses the audit logging already built into ONIX (based on OpenTelemetry). You change **configuration only; you don't need a new image**.

| File | Where it goes | What it does |
|---|---|---|
| [`onix/audit-fields.yaml`](onix/audit-fields.yaml) | Each participant's adapter config folder | The allow-list: the only fields that leave the adapter |
| [`onix/otelsetup.yaml`](onix/otelsetup.yaml) | Merged into each adapter config (seeker and provider) | Turns on audit export to the network's collector |
| [`collector/config.yaml`](collector/config.yaml) | The network's telemetry collector | Keeps only ONIX audit records, strips signatures, forwards to the reporting service |

## What leaves the adapter

Only the fields listed in `audit-fields.yaml` leave the adapter. These are:

* the Beckn context header: action, IDs, timestamp, sender and receiver;
* coordination metadata: service type, urgency, contract and commitment status, attendance and deviation reason code.

The participant's own adapter removes patient details, notes, documents and consent before export. The network applies the same list again before it stores anything.

These are **per-message** records. Sygnal v0.9 allows per-message instrumentation only on networks declared non-production, and only until the policy expires. Production networks report aggregates. See [Reporting and signals](../docs/concepts/reporting-and-signals.md).

## Set up a participant adapter

These steps work with any ONIX image that includes the `otelsetup` plugin. An example is the image used by the Beckn starter kit's [generic devkit](https://github.com/beckn/starter-kit/tree/main/generic-devkit).

1. **Copy `onix/audit-fields.yaml`** into the folder your adapters mount as `/app/config` (for the generic devkit, `generic-devkit/config/`). Use a local file, not a URL. If ONIX can't load its audit config at start-up, it exports the whole message.
2. **Add the `otelsetup` block** from `onix/otelsetup.yaml` to both adapter configs. Fill in the values your network operator gives you. Set `serviceName` to your subscriber ID plus `-bap` or `-bpp`.
3. **Restart the adapters and check** that each logs `audit config loaded`:

   ```bash
   docker logs onix-bap 2>&1 | grep -i "audit config loaded"
   docker logs onix-bpp 2>&1 | grep -i "audit config loaded"
   ```

   If the line is missing, check the `auditFieldsConfig` path. Also check that the file is inside the folder mounted as `/app/config`.
4. **Send any request.** It should appear on the network's dashboards within seconds.

If you are joining the [Sygnal Sandbox](../docs/build/sandbox.md), you get the collector address and the other network values when you join.

The exporter sends ordinary outbound HTTPS (OTLP/gRPC over TLS on port 443). Use the collector's host name, not its IP address, because the certificate is checked against the name. If the adapter logs `tls: first record does not look like a TLS handshake`, the endpoint points at the collector's unencrypted port instead of 443.

To turn it off, remove the `otelsetup` block or set `enableLogs: "false"`, and restart.

## Optional: care-pathway view

`audit-fields.yaml` includes some fields that are commented out: pathway, specialty and sub-specialty codes, the expected arrival window and outcome time. With these fields, a dashboard can show care pathways and whether care was on time. They reveal more about the patient's condition and timing, so turn them on only where the network's governance allows.

## Status

This configuration runs today on the demonstration network. It will become part of the packaged Sygnal Edge Adapter; see [Edge Adapter](../docs/components/edge-adapter.md).
