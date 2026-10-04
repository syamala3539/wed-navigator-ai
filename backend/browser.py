from playwright.async_api import async_playwright

async def execute_plan(plan):
    results=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True)
        page=await browser.new_page()
        try:
            for step in plan.get("steps", [])[:6]:
                action=step.get("action")
                if action=="search":
                    q=step.get("query","")
                    await page.goto("https://www.google.com/search?q="+__import__("urllib.parse").parse.quote(q), wait_until="domcontentloaded", timeout=25000)
                    await page.wait_for_timeout(1200)
                    links=await page.locator("a").evaluate_all("""els => els.map(a=>({title:(a.innerText||'').trim(),url:a.href})).filter(x=>x.title && /^https?:/.test(x.url)).slice(0,12)""")
                    results.append({"step":"search","query":q,"items":links})
                elif action=="open_result":
                    idx=max(0,int(step.get("index",0)))
                    previous=next((x for x in reversed(results) if x.get("step")=="search"),None)
                    if previous and previous["items"]:
                        target=previous["items"][min(idx,len(previous["items"])-1)]["url"]
                        await page.goto(target,wait_until="domcontentloaded",timeout=25000)
                        results.append({"step":"open_result","url":page.url,"title":await page.title()})
                elif action=="extract":
                    title=await page.title() if page.url!="about:blank" else ""
                    text=(await page.locator("body").inner_text())[:5000] if page.url!="about:blank" else ""
                    results.append({"step":"extract","url":page.url,"title":title,"text":text})
                elif action=="summarize":
                    results.append({"step":"summarize","note":"Review the extracted page content above."})
        finally:
            await browser.close()
    return results
