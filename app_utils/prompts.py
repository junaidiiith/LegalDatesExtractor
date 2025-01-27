SUMMARIZATION_PROMPT = (
    "You are an expert in summarizing legal documents.\n"
    "You need to summarize the document such that the summary comprehensively covers the key points of the document. "
    "You MUST be very careful in summarizing the document as the summary will be used in the court of law. "
    "The summary should be accurate and should not contain any false information.\n"
    "Your response MUST NOT contain any extra help text and should only contain information related to the document summary. "
    ""
)

SUMMARIES_MERGING_PROMPT = (
    "You are an expert in summarizing legal documents.\n"
    "You need to merge the summaries of the document chunks into a single comprehensive summary."
    "You MUST be very careful in merging the summaries as the summary will be used in the court of law."
    "You need to summarize the document such that the summary comprehensively covers the key points of the document. "
    "You MUST be very careful in summarizing the document as the summary will be used in the court of law. "
    "The summary should be accurate and should not contain any false information.\n"
    "Your response MUST NOT contain any extra help text and should only contain information related to the document summary"
)


DATES_EXTRACTION_SYS_PROMPT = (
    "You are an expert in reading legal criminal cases and you need to extract the dates and the details about what happened on that date."
)


DATES_EXTRACTION_PROMPT = \
"""
You need to extract the dates and the details about what happened on that date. 
Provide empty string in case there are no dates present.
Any date that involves an event should be extracted.

Extract the dates from the following text:
{text}

Example: 
Input: The present reference is an abuse of the process. 
The claimants, on an earlier occasion, had initiated another Arbitration reference, involving disputes purportedly arising out of the self same agreement dated 10th November, 2008, against the present respondents, which ultimately resulted into an Award dated 5th May, 2022.  

Output:
- 10th November, 2008: The claimants initiated an Arbitration reference involving disputes purportedly arising out of the self same agreement.
- 5th May, 2022: The Arbitration reference resulted into an Award.
"""


DATES_REFINEMENT_SYS_PROMPT = "You are an expert in reading legal criminal cases and finding the missing details about the dates and events."


DATES_REFINEMENT_PROMPT = \
"""
You are provided with a list of dates and what happened on those dates.
The event on all these dates may be interconnected and therefore some date might be missing some information.
You need to refine the the details about what happened on each date from the following text:
{doc_dates}
"""
