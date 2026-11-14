# M06-L02 — Should we invest in an AI support assistant?

Status: complete narration draft for editorial review; not yet recorded or expert-approved.
Target: approximately 10–11 minutes, including learner pause and visual holds. Measure synthesized speech before locking the timeline. Audience: business professionals who understand baselines and KPIs (M06-L01). All organization names and financial inputs below are fictional teaching assumptions, in USD. They are not AWS prices or a forecast.

Primary skills: 2.2.3, 2.2.5, 2.1.3. Supporting reinforcement: baselines, quality metrics and human oversight. Sources: aws-domain-2 and aws-domain-3 for scope and decision practices. Arithmetic and scenario are original.

Learning outcome: Given a baseline, cost assumptions and a quality constraint, calculate first-year ROI, identify the break-even condition and defend a bounded pilot recommendation.

## S01 — The decision, not the product

Northstar Services handles twelve thousand customer support tickets each month. Its service director proposes an AI assistant that drafts replies for human agents to review. The request is simple: should we invest?

A compelling demonstration is useful, but it does not answer the investment question. We need to connect the proposed capability to a business outcome, estimate all relevant costs, and identify what must be true for the investment to pay off.

By the end of this lesson, you will be able to calculate first-year return on investment, test a critical assumption, and recommend an experiment that protects customers while gathering better evidence. Keep a distinction in mind throughout: time released is potential capacity. It becomes financial value only when the organization can use it productively or avoid an actual cost.

## S02 — Establish the baseline and boundaries

Northstar's measured baseline is twelve minutes of agent handling time per ticket. The fully loaded labor rate is thirty dollars per hour. For this simplified example, ticket volume, labor rates and the baseline remain constant over the year.

That represents two thousand four hundred handling hours per month, with a labor-equivalent value of seventy-two thousand dollars. We are not claiming that all of this cost can disappear. It is the baseline against which a narrowly defined improvement will be measured.

The first release assists agents with eligible written responses. It does not send messages automatically, approve refunds or change customer accounts. Agents remain responsible for reviewing the answer. If the pilot adds review effort, that effort belongs in the calculation. Our time-saving assumption must be net of review and correction time.

## S03 — From time saved to usable value

Suppose early testing suggests a net saving of three minutes on each assisted ticket, and we assume that half of all tickets will actually receive assistance. Twelve thousand tickets, multiplied by fifty percent, multiplied by three minutes, divided by sixty, gives three hundred hours released each month.

At thirty dollars per hour, that is nine thousand dollars of potential monthly capacity value. Now make the business assumption visible: Northstar expects to turn seventy percent of that capacity into useful output or avoided cost. The recognized monthly benefit is therefore six thousand three hundred dollars.

The seventy percent is an illustrative realization factor, not an industry benchmark. It needs evidence. If the team cannot redeploy the capacity, reduce overtime or avoid additional hiring, the organization should report the time improvement separately rather than present the entire amount as cash savings. Do not count both the labor value and revenue from the same released hours without demonstrating that they are distinct benefits.

## S04 — Include the cost of operating the change

Northstar estimates recurring costs of three thousand dollars per month: eighteen hundred for the model or software, seven hundred for integration support, and five hundred for monitoring, evaluation and governance. One-time implementation and training costs total eighteen thousand dollars.

These are invented teaching inputs. In a real proposal, collect current vendor quotes and describe the usage assumptions behind them. A model's unit price alone does not represent the cost of a working business solution. Include retrieval or storage where relevant, operational support, security reviews, training and change management, and any additional human oversight.

For year one, recurring costs are thirty-six thousand dollars. Adding the one-time cost gives a total of fifty-four thousand. Our simplified model excludes taxes, discounting, financing and a separate ramp period; each exclusion should be reconsidered for a real investment. In particular, benefits rarely arrive at full scale on the first day.

## S05 — Calculate and interpret the base case

Annual recognized benefit is six thousand three hundred dollars times twelve: seventy-five thousand six hundred dollars. Subtract the fifty-four thousand dollars of first-year cost. The estimated first-year net benefit is twenty-one thousand six hundred dollars.

In this lesson, ROI means net benefit divided by total cost over the same period. Twenty-one thousand six hundred divided by fifty-four thousand gives forty percent first-year ROI. State the definition and time horizon because different organizations use different financial conventions.

The monthly recognized benefit less recurring cost is thirty-three hundred dollars. Dividing the eighteen-thousand-dollar upfront cost by that monthly amount gives a simple payback of about five and a half months after steady-state benefits begin. That is not necessarily five and a half months from contract signature. Implementation delay and adoption ramp can push the calendar payback later. This model is a decision aid, not a promise.

## S06 — Ask what could reverse the decision

Now test adoption. Suppose only twenty-five percent of tickets receive assistance, while the other assumptions remain unchanged. Recognized monthly benefit falls to three thousand one hundred fifty dollars. The first-year benefit becomes thirty-seven thousand eight hundred dollars. The first-year net result is a loss of sixteen thousand two hundred dollars, giving negative thirty percent ROI.

At seventy-five percent assisted-ticket coverage, the model gives one hundred thirteen thousand four hundred dollars of annual benefit and one hundred ten percent first-year ROI. These are sensitivity cases, not confidence intervals or probability estimates. Costs are held constant solely to isolate adoption; in reality, model usage costs may rise with assistance volume.

Under our simplified fixed-cost assumptions, first-year break-even requires around thirty-five point seven percent of all tickets to receive assistance. That is fifty-four thousand dollars divided by the annual benefit at full assistance and seventy percent realization. If adoption ramps slowly or costs increase with volume, the required steady-state coverage will be higher. A positive base case is therefore a reason to test critical assumptions, rather than immediate evidence for enterprise rollout.

## S07 — Measure value and protect customers

What should the pilot measure? Start with net handling time, including agent review and correction. Record assisted-ticket coverage using all tickets as the denominator, so the metric is comparable with our financial model. Also report coverage within eligible tickets to understand whether the workflow fits its intended use.

Pair speed with quality: resolution accuracy, repeat contacts, escalation rates and customer satisfaction. A shorter first interaction that generates a second contact can destroy the apparent saving. Evaluate a representative sample and examine important customer groups rather than relying on a few impressive outputs.

Use appropriate access controls, approved data and human review. Route sensitive or uncertain cases to an agent, and define a stop condition for serious safety or privacy failures. These controls address specific risks; they do not guarantee that the system will be error-free. An accountable owner must be able to pause the workflow and restore the existing process.

## S08 — Make a conditional recommendation

Recommend a bounded pilot before a full rollout. Agree on the baseline, comparison method, cost ceiling, quality guardrails and decision thresholds before results are available. A comparable control group or a carefully designed phased introduction can help distinguish the assistant's effects from seasonal workload or staffing changes. Have the appropriate analyst design the comparison and sample size.

Scale only if the evidence supports usable business value and acceptable quality. Pause to address low adoption or fixable workflow problems. Stop if material risks cannot be controlled or the economics remain unfavorable. Do not move a threshold simply because a pilot has already consumed money.

Northstar's recommendation is conditional: test whether the assistant can produce verified net savings, sufficient assisted-ticket coverage and a credible plan to realize the released capacity. Separately confirm that customer outcomes and required controls remain acceptable. An investment decision combines the economics with these constraints.

## S09 — Your decision and recap

Pause here and choose the strongest next step. A: purchase an enterprise contract because the base case has positive ROI. B: run a bounded pilot that measures net time saved, coverage, realized value, costs and quality. Or C: reject the proposal because the low-adoption case loses money.

The strongest answer is B. A treats assumptions as established results. C treats one sensitivity case as a prediction. A bounded pilot reduces uncertainty while keeping the decision reversible.

The transferable method is to establish a baseline, convert improvement into realizable value, include the full cost of change, and test the assumptions that can reverse the decision. Then apply explicit quality and risk conditions. For the exam, practice explaining why that recommendation fits the facts, rather than selecting the option with the most enthusiastic AI language.
