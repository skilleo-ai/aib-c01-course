# Lesson 01 — AI, ML and generative AI

Review draft. Skills 1.1.1 and 1.1.2; reinforces 1.2.1. Original synthetic examples. Independent exam preparation.

## s01 — AI, ML and generative AI

Imagine you're in a planning meeting at a retailer. One team wants to forecast next month's demand. Another wants to draft product descriptions. A third wants a ten percent discount applied to every order over one hundred dollars. Someone calls all three projects artificial intelligence. Should you treat them as the same kind of investment? Probably not. They produce different outputs, depend on different evidence, and need different checks. In this lesson, we'll separate artificial intelligence, machine learning, and generative AI, using decisions a business leader might actually face. You won't need to write code. Your job is to ask better questions about the work the system is meant to do.

## s02 — Start with the output

By the end, you should be able to explain how these terms fit together, classify a business use case, and choose what kind of evidence would demonstrate success. Start with one question: what output does the business need? Sometimes it's a fixed calculation. Sometimes it's a prediction, a category, or a recommendation. Sometimes it's a new piece of text, an image, or another form of content. That question is more useful than starting with a product name. A single business process can combine several of these capabilities, so we'll classify the individual tasks before we describe the whole solution.

## s03 — Artificial intelligence is the umbrella

Artificial intelligence is the broad field of building systems that perform tasks associated with intelligence, such as recognizing patterns, understanding language, reasoning, or making recommendations. It doesn't mean a computer thinks or understands in the same way a person does. And AI isn't limited to systems that learn from data. Some approaches use explicitly represented knowledge and rules. That's why we should avoid saying that every rule-based system is outside AI. For the retailer's simple discount calculation, though, ordinary deterministic automation is a sufficient description. Calling a basic formula AI doesn't make it a better investment. Describe what the system actually does and what capability the task requires.

## s04 — Machine learning learns from examples

Machine learning is a family of AI methods that learns patterns from data rather than requiring a person to specify every decision rule. Think about the demand forecast. Historical sales, promotions, prices, and seasonal patterns might help a model estimate future sales. Training is the process that uses data to learn the model's patterns or parameters. Inference is using the resulting model on an input to produce an output. The output might be a number, a category, a ranking, or a recommendation. Learning doesn't imply the model is correct, fair, or ready for production. Those claims need evaluation using relevant evidence. We'll examine training and inference more closely in the next lesson.

## s05 — A forecast needs a meaningful baseline

Let's make the forecast concrete. The retailer asks: how many winter jackets should we stock next month? A machine learning model can estimate a quantity using patterns in relevant data. But a prediction is an estimate, not a guaranteed future outcome. If customer behavior changes or the data misses a major promotion, performance can deteriorate. To evaluate the proposal, compare forecasts with actual demand on suitable held-out or future data. Also compare with a sensible existing approach, such as the current forecasting process. Better model accuracy matters only if it supports a business outcome, such as fewer stockouts without excessive inventory. A convincing demonstration alone doesn't establish that value.

## s06 — Generative AI creates content

Generative AI creates content, such as text, images, audio, or code, using patterns learned from data. Modern generative AI systems are built with machine learning, often using large neural networks. For business classification, distinguish generating content from estimating a target such as next month's sales. The technical boundary is more subtle: a language model itself predicts tokens as it generates text. So when we say prediction versus generation here, we're describing the business task and output, not claiming that the underlying mathematics never overlaps. A fluent response is also not proof of factual correctness. Generating plausible language and verifying a product claim are different responsibilities.

## s07 — Drafting a description is generation

Now the marketing team wants a product description for a new winter jacket. A generative AI system can draft copy from an approved product record and a style instruction. Success isn't measured in the same way as a demand forecast. Review whether the copy preserves product facts, follows the intended tone, avoids unsupported claims, and is useful to customers. If the jacket isn't waterproof, polished wording must not imply that it is. Human review or other appropriate checks should match the risk of publishing an error. You can also measure net drafting time, including the time spent reviewing and correcting the output. Fast generation doesn't automatically mean the complete workflow saves time.

## s08 — The terms overlap

Here's the relationship to remember. Artificial intelligence is the broad umbrella. Machine learning is one important part of it. The modern generative AI systems we're discussing use machine learning to generate content. So the same product can accurately be described as AI, machine learning, and generative AI. These are not three competing vendors or three mutually exclusive purchasing categories. At the same time, many machine learning applications are not primarily generative: a fraud classifier or a demand forecaster has a different business purpose. Use the more specific description when it helps clarify the output, the evidence, and the risks. Avoid choosing a capability just because the broadest label sounds impressive.

## s09 — Use the simplest suitable approach

Return to the discount. The policy is unambiguous: if an eligible order exceeds one hundred dollars, apply ten percent off. A fixed rule is transparent and easy to test against known cases. You don't need a learned model to infer a policy the business has already specified. That doesn't mean rules are always simple or that AI can never use rules. It means this task has an explicit, stable relationship between input and expected output. If the business later wants to personalize offers based on response patterns, that's a different problem. Revisit the requirements rather than automatically replacing every rule with a model.

## s10 — One workflow can combine all three

Real products often combine capabilities. The retailer might use machine learning to forecast demand, an explicit business rule to flag low stock, and generative AI to draft a buyer's summary. Calling the whole workflow a generative AI solution can hide important dependencies. If a summary reads well but the forecast is unreliable, the process can still make a bad purchasing recommendation. Evaluate each component and the end-to-end outcome. Ask what data enters each stage, who can act on the output, and what happens when a component is wrong. This task-level view helps business leaders discuss the proposal clearly with technical teams without needing to choose algorithms or configure services.

## s11 — Match the evidence to the task

Here's a practical way to review a proposal. First, ask what output the task needs. Second, ask whether that output follows an explicit rule or depends on learned patterns. Third, ask how success will be evaluated in the actual business process. For the discount, test the calculation and policy boundary cases. For the forecast, evaluate error against an appropriate baseline and measure inventory effects. For product copy, evaluate factual accuracy and suitability, alongside the time needed to review it. None of these checks is replaced by an impressive demo or a confident vendor claim. The capability label helps organize the discussion; evidence supports the decision.

## s12 — Your turn: classify the task

Let's try three short examples. A: a system calculates tax using a rate and rules supplied by finance. B: a system learns from historical customer behavior to estimate the probability of churn. C: a system drafts a customer email using an approved offer and a tone instruction. Which is best described as ordinary rule-based automation, which as predictive machine learning, and which as generative AI? Think about the task's output rather than whether the interface looks modern. I'll give you a moment to decide.

## s13 — Answers—and the reasoning

A is ordinary rule-based automation in this scenario: the calculation applies a specified policy. B is predictive machine learning: the system learns from historical data to estimate a probability. C is generative AI: it creates an email draft from instructions and context. That draft still needs checks for offer accuracy and appropriateness. B and C both use machine learning in the modern systems we've described, but they serve different business purposes. If you classified by output and explained the evidence each task needs, you've understood the central distinction. If you only memorized three labels, return to the examples and explain why each choice fits.

## s14 — Ask better questions about AI

Let's bring this together. AI is the broad field. Machine learning learns patterns from data. Modern generative AI uses learned patterns to create content. Ordinary deterministic automation remains useful when the business can specify a suitable rule. These descriptions help you ask what the system produces, what evidence would make it trustworthy for its purpose, and whether the capability is worth using. For your own workplace, choose one task and write down its required output, the simplest suitable approach, and how you'd evaluate success. In the next lesson, we'll build on this foundation by separating training from inference and examining what historical data can and cannot prove.
