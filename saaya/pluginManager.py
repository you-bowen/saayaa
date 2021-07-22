from __future__ import annotations
from saaya.event import Event
from collections import defaultdict as ddict
from saaya.logger import logger
from saaya.utils import FingerPrints
import asyncio


class BaseManager:
    plugins = {}

    def __init__(self):
        self.plugins = ddict(lambda: 0, {
            'OnLoad': []
        })
        # 这里一般使用'指纹'来添加事件类型
        # 你也可以手动添加事件类型，比如'Onload'

    async def broadCast(self, event: Event):
        """
        拥有'aaa.bbb.admin'指纹的event
        会先找对应的'aaa.bbb.admin'类型
        再找'aaa.bbb'类型
        再找'aaa'类型
        """
        origin_fp = event.fingerprint
        fps = FingerPrints(origin_fp)
        task_list = []
        for fp in fps:
            if self.plugins[fp] != 0:
                for plugin in self.plugins[fp]:
                    logger.debug("broadCast to: "+str(plugin))
                    task_list.append(asyncio.create_task(plugin(event)))
                await asyncio.wait(task_list)

    def registerEvent(self, fingerprint: str):
        def plugin(func):
            logger.debug(f'Registering {func} on {fingerprint}')
            if self.plugins[fingerprint] == 0:
                self.plugins[fingerprint] = []
            self.plugins[fingerprint].append(func)

        return plugin


PluginManager = BaseManager()
