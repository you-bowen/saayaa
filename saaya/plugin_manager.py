
from __future__ import annotations
from saaya.event import Event
from collections import defaultdict as ddict
from saaya.logger import logger
import asyncio


class Base_manager:
    def __init__(self):
        self.plugins = ddict(list, {
            "Boot": [],
        })
        # 这里一般使用'指纹'来添加事件类型
        # 你也可以手动添加事件类型，比如'Onload'
        self.strip = lambda x : x[:x.rfind('.')]

    def split_fp(self, fp):
        """
        turn 'a.b.c' -> ['a.b.c','a.b','a']
        """
        fps = []
        while(fp):
            fps.append(fp)
            fp = self.strip(fp)
        return fps


    async def broadcast(self, event: Event):
        """
        fp : 'aaa.bbb.admin'
        fps: ['aaa.bbb.admin', 'aaa.bbb', 'aaa']
        """
        fps = self.split_fp(event.fingerprint)
        for fp in fps:
            if self.plugins[fp]:
                logger.debug(f"broadcast to: `{event.fingerprint}` plugins...")
                await asyncio.gather(*[
                    plugin(event) for plugin in self.plugins[fp]
                ])

    def reg_event(self, fingerprint: str):
        def plugin(func):
            logger.debug(f'Registering {func} on {fingerprint}')
            self.plugins[fingerprint].append(func)
        return plugin
    
    
    # def reg_boot_event(self, func):
    #     self.boot_plugins["Boot"].append(func)


plugin_manager = Base_manager()