---
description: Other industries solved coordination between organisations that share no database and no owner.
---

# You've seen this idea before

Other industries have solved this exact problem: coordinating a handoff, and spotting the gap, between organisations that share no database and no owner.

* **Parcel and freight tracking.** This is the closest everyday parallel. A parcel moves between carriers, depots and couriers that each run their own systems. A shared tracking number carries the handoff, and an exception system knows when a package misses a checkpoint, without any single party owning the truck, the warehouse or the goods in the box. In health, getting a patient to the next step is a delivery problem too.
* **Airline interline baggage.** When a bag transfers between two airlines on a connecting flight, a shared handoff system confirms the transfer. Neither airline needs the other's full operations data to know the bag arrived, or to know when it didn't.
* **Payment networks.** Banks that share no database move money between each other every second. Shared rules and messages coordinate them, not one owner's system. Real-time networks such as UPI in India and Pix in Brazil show this can run as public infrastructure.
  * **Spotting problems without seeing the contents.** Card networks watch patterns across thousands of unrelated merchants and banks (where, when, how much) and flag unusual activity in real time, without ever seeing what was bought.

## One analogy for the whole: air traffic control

Air traffic control is the closest complete parallel. It has independent operators, coordinated handoffs, a shared picture, and controllers who never fly the plane. Each part of a Sygnal network has a counterpart in it.

| Part of a Sygnal network | In air traffic control | In health |
|---|---|---|
| **Edge adapter** | **The transponder on every aircraft.** Any plane, from any airline, emits the same signal, and any controller can receive it. Nothing about the cabin, the cargo or the passengers travels with it. | An adapter on whatever platform a facility already runs. |
| **Coordination protocol** | **The controller.** Watches many aircraft at once and acts: hands an aircraft from one sector to the next and confirms that each handoff was accepted. This is why a map alone isn't coordination. | Handoffs carried between platforms and confirmed by both sides. |
| **Policy** | **The rulebook.** Minimum distances between aircraft, approach procedures and that country's airspace rules are set in advance, not invented for each flight. | The health system's coordination rules and service-level agreements (SLAs), checked instantly, much as a spellchecker checks text. |
| **Network Intelligence** | **The radar picture.** Position, speed and heading: enough to see the whole system at once, and nothing about who is on board. | The pattern across thousands of coordination events. |

Public flight-tracking websites exist because the same open feed goes to everyone. That shared picture is possible only because the coordination underneath runs on an open protocol, which is exactly the argument for building health coordination the same way.
