---
description: Health systems know more than they act on. The gap is follow-through, not data.
---

# The coordination gap

## Health systems know more than they act on

Health systems have invested heavily in health data, and that investment has worked. Records are shared, health information exchanges are live, and standards such as FHIR are widely adopted. Platforms can and do pass records to one another.

Yet there is little evidence that more data, on its own, produces better care. A systematic review of health information exchange found 34 studies of its outcomes, and **not one measured an effect on mortality or morbidity**. Where clinicians did report improvement, they said it came from better coordination, communication and knowledge of the patient, not from the exchange of records itself ([Hersh et al., 2015](https://medinform.jmir.org/2015/4/e39/)).

A study of the US regions furthest ahead on health IT found that the gaps clinicians described were **coordination gaps**: a referral whose outcome never came back, a follow-up nobody owned. These gaps persisted even in the places with the most mature data infrastructure. Sharing data between systems did not, by itself, coordinate the people using them ([Samal et al., 2016](https://doi.org/10.1186/s12913-016-1373-y)).

So the constraint is not how much a health system knows. It is what none of its platforms pass along: **what should happen next**. A record tells you what happened. It does not tell anyone that a referral was never completed, or that a woman who was told to come back never did.

Every patient who falls through that gap becomes a **ghost patient**: present in the data, absent from the care.

## The size of the gap

| | |
|---|---|
| **36%** compound annual growth of health data, globally | Health data is the fastest-growing kind of data across the industries IDC tracks. Volume is not the constraint (IDC, 2018). |
| **5 million** deaths a year from poor-quality care in low- and middle-income countries | Each year, 8.6 million people die from conditions that health care could have treated. Of these, 5 million (58%) are attributed to poor-quality care among people who had already reached the health system, and 3.6 million to lack of access ([Kruk et al., 2018](https://pubmed.ncbi.nlm.nih.gov/30195398/)). |
| **US$27–78 billion** a year lost to failures of care coordination, in the United States alone | This is one item within an estimated US$760–935 billion of total health-system waste, in a highly digitised health system ([Shrank et al., 2019](https://jamanetwork.com/journals/jama/fullarticle/2760715)). |

## Why integrations alone don't close it

Today, coordinating care across platforms usually means **point-to-point integration**: every pair of platforms that needs to hand off a patient builds and maintains its own bridge. This leads to three problems:

* **Integration work multiplies.** Each new platform needs bridges to many others: up to N×(N−1)/2 for N platforms, and each breaks when either side changes.
* **No one owns the follow-through.** A referral raised in the field, the follow-up three days later, the escalation to a facility and the outcome returning to the original worker span several platforms and several days. No single integration owns that thread, so no one notices when it breaks.
* **No one can see the whole picture.** Simple questions such as "what share of referrals in this district were completed?" have no answer, because nothing collects that information across platforms.

The result is coordination that is manual, loses information and cannot be seen. [How Sygnal helps](how-sygnal-helps.md) describes the alternative.

## Sources

1. Hersh WR, Totten AM, Eden KB, et al. "[Outcomes From Health Information Exchange: Systematic Review and Future Research Needs](https://medinform.jmir.org/2015/4/e39/)." *JMIR Medical Informatics*. 2015;3(4):e39.
2. Samal L, Dykes PC, Greenberg JO, et al. "[Care coordination gaps due to lack of interoperability in the United States: a qualitative study and literature review](https://doi.org/10.1186/s12913-016-1373-y)." *BMC Health Services Research*. 2016;16:143.
3. Reinsel D, Gantz J, Rydning J. *Data Age 2025: The Digitization of the World, From Edge to Core*. IDC white paper, sponsored by Seagate. November 2018.
4. Kruk ME, et al. "[Mortality due to low-quality health systems in the universal health coverage era: a systematic analysis of amenable deaths in 137 countries](https://pubmed.ncbi.nlm.nih.gov/30195398/)." *The Lancet*. 2018;392:2203–2212.
5. Shrank WH, Rogstad TL, Parekh N. "[Waste in the US Health Care System: Estimated Costs and Potential for Savings](https://jamanetwork.com/journals/jama/fullarticle/2760715)." *JAMA*. 2019;322(15):1501–1509.
