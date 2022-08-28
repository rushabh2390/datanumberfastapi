import aiohttp


async def get_fact_from_number_Api_by_Month_n_date(month: int, day: int):
    """call number resource api for date fact for given month and day

    Args:
        month (int): month value (1-12)
        day (int): day value(1-31)

    Returns:
        _type_: description on that particalr day and month from number api
    """
    description = ""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://numbersapi.com/"+str(month)+"/"+str(day)+"/date") as resp:
                description = await resp.text()
    except Exception as e:
        return None, "Exception: " + str(e)
    return description, None
