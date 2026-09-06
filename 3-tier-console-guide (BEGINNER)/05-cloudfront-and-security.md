# Add CloudFront, HTTPS, Origin Protection, and Rate Protection

## Estimated Time

60–100 minutes, including CloudFront and AWS WAF deployment time

## Lecture Outcome

You will create a CloudFront distribution, redirect viewers to HTTPS, support dynamic API requests correctly, require an origin-verification header, restrict the ALB to CloudFront origin-facing addresses, and protect the unauthenticated booking endpoint with a baseline AWS WAF rate rule.

## Prerequisites

- The ALB URL loads the application and `/health` returns HTTP `200`.
- All expected targets are Healthy.
- You recorded the ALB DNS name.

## Cost Impact

> **Cost warning:** CloudFront requests and transfer are billable, and the required AWS WAF Web ACL and rule add charges. Check current CloudFront and AWS WAF prices before continuing, use only the bounded validation traffic in this lecture, and complete the cleanup lecture.

## Important TLS Limitation

> **Important:** This lab encrypts traffic from the viewer to CloudFront. The CloudFront-to-ALB hop uses HTTP because the generated ALB DNS name cannot be covered by your own ACM certificate. For end-to-end TLS, use a custom domain, request an ACM certificate that matches the origin domain, add an HTTPS listener to the ALB, and set the CloudFront origin protocol to HTTPS only.

## Action 1: Generate an Origin-Verification Value

Generate 32–64 random ASCII alphanumeric characters using only A–Z, a–z, and 0–9. Do not reuse a password or API key. Do not include punctuation; in particular, `*` and `?` are forbidden because they can be interpreted specially in matching fields. A generic password generator may insert punctuation that is invalid for this instruction or has special matching behavior, so configure it for ASCII letters and digits only and verify the result before saving it.

- Header name: `X-Origin-Verify`
- Header value: ______________________________

> **Security note:** Treat this as configuration data. Do not include it in screenshots or public project submissions.

## Action 2: Create the CloudFront Distribution

1. Open CloudFront.
2. Choose Create distribution.
3. For Origin domain, select or enter the ALB DNS name.
4. Configure the origin:

   | Setting | Value |
   |---|---|
   | Origin protocol | HTTP only |
   | HTTP port | `80` |
   | Minimum origin SSL protocol | Not applicable for HTTP-only origin |
   | Origin name | `3tier-app-alb-origin` |

5. Add a custom origin header:

   | Setting | Value |
   |---|---|
   | Header name | `X-Origin-Verify` |
   | Value | Your generated value |

6. Configure the default cache behavior:

   | Setting | Value |
   |---|---|
   | Path pattern | Default (`*`) |
   | Viewer protocol policy | Redirect HTTP to HTTPS |
   | Allowed HTTP methods | GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE |
   | Cache policy | CachingDisabled |
   | Origin request policy | AllViewerExceptHostHeader, or the equivalent managed policy shown by the console |
   | Compress objects automatically | Yes |

7. Keep query strings, cookies, and required request headers forwarded through the selected origin request policy.
8. Use the default CloudFront certificate for the generated `cloudfront.net` domain.
9. Set a description such as Three-tier application distribution.
10. Add the standard tags and create the distribution.
11. Wait until the distribution status is Deployed.

### Why Caching Is Disabled

The supplied application has dynamic APIs and creates bookings with POST requests. Disabling caching prevents one user from receiving stale or inappropriate dynamic responses. A production design would create separate cache behaviors for immutable static assets and dynamic API paths.

## Action 3: Test CloudFront Before Locking the Origin

1. Copy the distribution domain name.
2. Open:

   `https://<DISTRIBUTION_DOMAIN>`

3. Confirm the page loads over HTTPS.
4. Open:

   `http://<DISTRIBUTION_DOMAIN>`

5. Confirm the browser redirects to HTTPS.
6. View events and create a test booking with placeholder data.
7. Open `/health` through the distribution and confirm it is healthy.

> **Important:** Do not continue until these tests pass.

## Action 4: Require the Origin Header at the ALB

The listener currently forwards every request. Change it so only requests with CloudFront’s custom header reach the target group.

1. Open EC2, Load Balancers, and select `3tier-app-alb`.
2. Open Listeners and rules.
3. Select the `HTTP:80` listener and manage rules.
4. Add a rule with priority 1:

   | Setting | Value |
   |---|---|
   | Condition | HTTP header |
   | Header name | `X-Origin-Verify` |
   | Header value | Your generated value |
   | Action | Forward to `3tier-app-target-group` |

5. Change the default action to Return fixed response:

   | Setting | Value |
   |---|---|
   | Status code | `403` |
   | Content type | `text/plain` |
   | Response body | Forbidden |

6. Save the listener rules.
7. Before changing the security group, test both paths:

   | Path | Expected result |
   |---|---|
   | CloudFront URL | should still load the application |
   | Direct ALB URL | should return HTTP `403` from the listener |

8. Capture the `403` result now. After network restriction, a direct request will normally time out instead of reaching the listener.

## Checkpoint

The listener forwards CloudFront requests carrying the header and returns `403` to header-less requests that can still reach it.

## Action 5: Restrict the ALB Security Group to CloudFront

The header check provides application-layer origin protection. Add network-layer restriction as defense in depth.

1. Open VPC, Managed prefix lists.
2. Find the AWS-managed prefix list named:

   `com.amazonaws.global.cloudfront.origin-facing`

3. Copy its prefix list ID.
4. Open Security Groups and select `3tier-app-alb-sg`.
5. Edit inbound rules.
6. Remove the temporary HTTP rule from `0.0.0.0/0`.
7. Add:

   | Setting | Value |
   |---|---|
   | Type | HTTP |
   | Port | `80` |
   | Source | Prefix list, `com.amazonaws.global.cloudfront.origin-facing` |
   | Description | HTTP from CloudFront origins only |

8. Save the rule.
9. Retest the CloudFront URL; it must still work.
10. Retest the direct ALB URL. It should now be network-blocked and normally time out because your browser is not in the CloudFront origin-facing prefix list.

> **Important:** If the rule exceeds your security-group quota because the managed prefix list has a high rule weight, restore the temporary rule only long enough to avoid an outage, request a quota increase, and retain the origin-header requirement. Do not silently leave the origin open.

## Action 6: Create the Baseline AWS WAF Rate Rule

POST `/api/bookings` is intentionally unauthenticated for this teaching application. Rate protection is therefore a required baseline action, not an extension.

1. Open AWS WAF and choose Create web ACL.
2. Select the CloudFront distributions resource type. CloudFront-scope AWS WAF resources are managed in the global CloudFront scope; the console may direct you to `us-east-1`.
3. Enter:

   | Setting | Value |
   |---|---|
   | Web ACL name | `3tier-app-web-acl` |
   | Associated AWS resource | Your project CloudFront distribution |
   | Default web ACL action | Allow |

4. Add your own rules and rule groups, then choose a rule builder for a rate-based rule.
5. Configure:

   | Setting | Value |
   |---|---|
   | Rule name | `3tier-app-booking-rate-limit` |
   | Rule type | Rate-based rule |
   | Rate limit | 20 |
   | Evaluation window | 5 minutes |
   | Request aggregation | Source IP address |
   | Action | Block |

6. Add a scope-down statement with AND logic so the rate applies only when both conditions are true:

   ### Statement 1

   | Setting | Value |
   |---|---|
   | Inspect | HTTP method |
   | Match type or positional constraint | Exactly matches string |
   | Value | POST |
   | Text transformation | None |

   ### Statement 2

   | Setting | Value |
   |---|---|
   | Inspect | URI path |
   | Match type or positional constraint | Exactly matches string |
   | Value | `/api/bookings` |
   | Text transformation | None |

7. Enable the rule’s CloudWatch metrics and sampled requests, keeping the suggested metric name if the console supplies one.
8. Review the rule. Confirm it blocks only POST requests whose URI path is exactly `/api/bookings`.
9. Create the Web ACL and associate it with the project CloudFront distribution if it was not associated during creation.
10. Wait until the Web ACL and distribution association show an active or deployed status.

> **Important:** The limit of 20 requests per source IP in five minutes is a conservative teaching threshold, not a production recommendation. A school, office, VPN, or hosted lab can place many learners behind one shared egress IP, causing their requests to aggregate. Coordinate with your instructor and classmates before validating the rule.

## Action 7: Validate the WAF Rule With Bounded Traffic

> **Important:** Use placeholder data and coordinate before testing in a shared classroom.

1. First, create exactly one legitimate booking through the CloudFront application and confirm it succeeds. If it fails, troubleshoot before sending any validation requests.
2. From a terminal, set the distribution domain without `https://`:

   ```bash
   DISTRIBUTION_DOMAIN=<YOUR_DISTRIBUTION_DOMAIN>
   ```

3. Run this bounded command. It sends no more than 25 invalid empty-object POST requests, and each request that reaches the application receives HTTP `400` without creating a booking. The loop stops after the first AWS WAF HTTP `403` response:

   ```bash
   for i in $(seq 1 25); do status=$(curl -sS -o /dev/null -w '%{http_code}' -H 'Content-Type: application/json' --data '{}' "https://${DISTRIBUTION_DOMAIN}/api/bookings"); printf 'request %s: HTTP %s\n' "$i" "$status"; [ "$status" = "403" ] && break; sleep 1; done
   ```

4. Confirm the early responses are application HTTP `400` responses and later requests receive an AWS WAF HTTP `403` block. Rate-based enforcement and metric display can take a short time, so do not increase or repeat the bounded loop to force an immediate result.
5. Open AWS WAF, select `3tier-app-web-acl`, then review sampled requests and the `3tier-app-booking-rate-limit` rule metrics. Confirm the matching POST `/api/bookings` requests and blocked requests become visible.
6. Stop after the first WAF block. Wait out the full five-minute evaluation window before any further booking tests; in a shared classroom, wait for the instructor to confirm that the shared source IP is no longer rate-limited.

> **Warning:** Never run an unbounded loop or general-purpose load generator against the endpoint. If 25 requests produce only HTTP `400` responses, stop anyway and use the troubleshooting checks below rather than sending more traffic.

## Action 8: Review the Complete Security Path

Confirm:

- [ ] Viewer to CloudFront uses HTTPS.
- [ ] CloudFront sends the origin header.
- [ ] The ALB security group accepts port `80` only from the CloudFront origin-facing prefix list.
- [ ] The ALB listener forwards only when the header matches.
- [ ] Direct browser traffic to the ALB is blocked at the network layer.
- [ ] `3tier-app-web-acl` is associated with the distribution.
- [ ] `3tier-app-booking-rate-limit` blocks excessive POST requests to exactly `/api/bookings` by source IP.
- [ ] The application security group accepts port `5000` only from the ALB security group.
- [ ] The database security group accepts port `3306` only from the application security group.
- [ ] EC2 and RDS have no public IP addresses.
- [ ] There is no inbound SSH rule.
- [ ] The application uses its schema-scoped runtime secret and verified RDS TLS.

## Optional Extension: End-to-End TLS

1. Use a domain you control.
2. Request or import an ACM certificate for the ALB origin domain in the ALB’s Region.
3. Create an `HTTPS:443` ALB listener.
4. Change CloudFront to HTTPS-only for origin requests.
5. For the CloudFront viewer certificate, request the certificate in `us-east-1` as required by CloudFront.
6. Update Route 53 DNS records and test certificate renewal and hostname matching.

## Save These Values

- CloudFront distribution ID: ______________________________
- CloudFront domain: ______________________________
- CloudFront managed prefix list ID: ______________________________
- Origin-verification header stored securely: Yes / No
- Listener returned `403` before SG restriction: Yes / No
- Direct ALB access is network-blocked after SG restriction: Yes / No
- WAF Web ACL name: `3tier-app-web-acl`
- WAF rate-rule name: `3tier-app-booking-rate-limit`
- WAF association status active/deployed: Yes / No
- WAF bounded validation status: Passed / Needs review

## Troubleshooting

### CloudFront Returns 502 Bad Gateway

Confirm the origin protocol is HTTP only on port `80` and the ALB listener is active.

### CloudFront Returns 403 After Listener Changes

Confirm the custom origin header name and value exactly match the ALB rule. Header matching is case-insensitive for the name but the value must match. Also check whether AWS WAF sampled the request and identify the terminating rule.

### POST Requests Fail

Confirm all required HTTP methods are allowed, the cache policy is CachingDisabled, and `3tier-app-booking-rate-limit` matches only POST with the exact `/api/bookings` path. If you just ran the bounded validation, wait out the five-minute evaluation window before testing again.

### The WAF Rule Never Blocks During the Bounded Validation

Do not send more than 25 requests. Confirm `3tier-app-web-acl` is associated with the correct distribution and active, the rule is enabled with Block action, aggregation is source IP, the evaluation window is five minutes, the limit is 20, and both exact-match scope-down statements are joined with AND. Allow time for rate enforcement and sampled requests to appear.

### Learners Are Blocked Before Completing Their Own Validation

A shared NAT, VPN, or classroom egress IP can aggregate requests from multiple learners. Stop all tests, coordinate with the instructor, and wait out the evaluation window before trying one legitimate booking.

### The Application Works Through the ALB but Not CloudFront

Check distribution deployment status, origin DNS name, origin port, custom header, ALB security-group source, WAF association, and the terminating WAF rule in sampled requests.

### The Managed Prefix List Is Unavailable

Confirm you are viewing the project Region. If the feature or quota is unavailable, retain header protection and document the limitation.

## Knowledge Check

1. Why is the ALB listener default action a `403` response?

   **Expected answer:** Requests that do not carry CloudFront’s origin-verification header should not reach the application.

2. Why is caching disabled for the default behavior?

   **Expected answer:** The default path includes dynamic and state-changing API operations that must not return cached user responses.

3. Why is the booking rate rule a baseline control?

   **Expected answer:** POST `/api/bookings` is unauthenticated, so a bounded source-IP rate control reduces basic automated abuse while learners evaluate stronger production controls.

4. Does HTTPS to CloudFront automatically mean HTTPS to the ALB?

   **Expected answer:** No. Viewer and origin connections are configured separately.

## Next Lecture

Create regional and edge notifications, seven alarms, and a dashboard, then run functional, resilience, and security validation.
