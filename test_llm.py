import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

passage = """
Trauma Does Not Exist

youth: If you are going to state things so forcibly, I’d like a thorough explanation. To begin with, what is the difference you refer to between etiology and teleology?

PHILOSOPHER: Suppose you've got a cold with a high fever, and you go to see the doctor. Then, suppose the doctor says the reason for your sickness is that yesterday, when you went out, you weren't dressed properly, and that’s why you caught a cold. Now, would you be satisfied with that?

yout: Of course | wouldn't. It wouldn’t matter to me what the reason was—the way | was dressed or because it was raining or whatever. It’s the symptoms, the fact that I’m suffering with a high fever now that would matter to me. If he’s a doctor, I’d need him to treat me by prescribing medicine, giving shots, or taking whatever specialized measures are necessary.

PHILOSOPHER: Yet those who take an etiological stance, including most counselors and psychiatrists, would argue that what you were suffering from stemmed from such-and-such cause in the past, and would then end up just consoling you by saying, “So you see, it’s not your fault.” The argument concerning so-called traumas is typical of etiology.

youTtH: Wait a minute! Are you denying the existence of trauma altogether?

PHILOSOPHER: Yes, | am. Adamantly.

YyouTtH: What! Aren’t you, or | guess | should say Adler, an authority on psychology?

PHILOSOPHER: In Adlerian psychology, trauma is definitively denied. This was a very new and revolutionary point. Certainly, the Freudian view of trauma is fascinating. Freud’s idea is that a person’s psychic wounds (traumas) cause his or her present unhappiness. When you treat a person’s life as a vast narrative, there is an easily understandable causality and sense of dramatic development that creates strong impressions and is extremely attractive. But Adler, in denial of the trauma argument, states the following: “No experience is in itself a cause of our success or failure. We do not suffer from the shock of our experiences—the so-called trauma—but instead we

make out of them whatever suits our purposes. We are not determined by our experiences, but the meaning we give them is self-determining.”

YOUTH: So we make of them whatever suits our purposes?

PHILOSOPHER: Exactly. Focus on the point Adler is making here when he refers to the self being determined not by our experiences themselves, but by the meaning we give them. He is not saying that the experience of a horrible calamity or abuse during childhood or other such incidents have no influence on forming a personality; their influences are strong. But the important thing is that nothing is actually determined by those influences. We determine our own lives according to the meaning we give to those past experiences. Your life is not something that someone gives you, but something you choose yourself, and you are the one who decides how you live.

YOUTH: Okay, So you’re saying that my friend has shut himself in his room because he actually chooses to live this way? This is serious. Believe me, it is not what he wants. If anything, it’s something he was forced to choose because of circumstances. He had no choice other than to become who he is now.

PHILOSOPHER: No. Even supposing that your friend actually thinks, / can’t fit into society because | was abused by my parents, it’s still because it is his goal to think that way.

youTH: What sort of goal is that?

PHILOSOPHER: The immediate thing would probably be the goal of “not going out.” He is creating anxiety and fear as his reasons to stay inside.

YOUTH: But why doesn’t he want to go out? That's where the problem resides.

PHILOSOPHER: Well, think of it from the parents’ view. How would you feel if your child were shut up in a room?

YOUTH: I'd be worried, of course. I'd want to help him return to society, Il’d want him to be well, and I’d wonder if I’d raised him improperly. I’m sure | would be seriously concerned and try in every way imaginable to help him back to a normal existence.

PHILOSOPHER: /hat is where the problem is. YOUTH: Where? PHILOSOPHER: If | stay in my room all the time, without ever going out,

my parents will worry. | can get all of my parents’ attention focused on me. They’ll be extremely careful around me and always handle

me with kid gloves. On the other hand, if | take even one step out of the house, I'll just become part of a faceless mass whom no one pays attention to. I'll be surrounded by people | don’t know and just end up average, or less than average. And no one will take special care of me any longer . . . Such stories about reclusive people are not uncommon.

YouTH: In that case, following your line of reasoning, my friend has accomplished his goal and is satisfied with his current situation?

PHILOSOPHER: | doubt he’s satisfied, and I’m sure he’s not happy either. But there is no doubt that he is also taking action in line with his goal. This is not something that is unique to your friend. Every one of us is living in line with some goal. That is what teleology tells us.

YOUTH: No way. | reject that as completely unacceptable. Look, my friend is—

PHILOSOPHER: Listen, this discussion won’t go anywhere if we just keep talking about your friend. It will turn into a trial in absentia, and that would be hopeless. Let’s use another example.

YOUTH: Well, how about this one? It’s my own story about something | experienced yesterday.

PHILOSOPHER: Oh? I’m all ears
"""

prompt = f"""
You are Deep Read, an AI tool that tests whether someone
actually understood a non-fiction book.

Analyze the passage below and generate exactly 5 questions.

The questions must test understanding, not simple memory.

Use these five question types:

1. Core argument
2. Conceptual distinction
3. Reasoning
4. Interpretation
5. Application

For each question:
- Give the question.
- Give four possible answers.
- Identify the correct answer.
- Give a short explanation of why it is correct.

Do not ask questions whose answers can simply be copied
from one sentence of the passage.

The questions should require the reader to understand
the author's reasoning.

PASSAGE:
{passage}
"""
response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt
)

print(response.text)
