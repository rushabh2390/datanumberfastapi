import aiohttp


async def get_fact_from_number_Api_by_Month_n_date(month: int, day: int):
    """_summary_

    Args:
        month (int): month value (1-12)
        day (int): day value(1-31)

    Returns:
        _type_: description on that particalr day and month from number api
    """
    description = ""
    
    async with aiohttp.ClientSession() as session:
        async with session.get("http://numbersapi.com/"+str(month)+"/"+str(day)+"/date") as resp:
            description = await resp.text()
    
    return description
