from pipeline.agents import csv_reader_agent
from pipeline.graph import build_graph
from pipeline.errors import PipelineError

async def run_pipeline(csv_path: str, source_type: str):
    graph = build_graph()
    records = csv_reader_agent(csv_path, source_type)

    results = []
    for state in records:
        #final_state = await graph.ainvoke(state)
        #results.append(final_state)

        try:
            #added config for conversational memory#removed memory not needed as such for this usecase
            #final_state = await graph.ainvoke(state, config={"configurable": {"thread_id": state["source_id"]}})
            final_state = await graph.ainvoke(state)
            results.append(final_state)
        except PipelineError:
            state["processing_log"].append("Pipeline failed for this record")
            results.append(state)

    return results
