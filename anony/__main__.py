# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic


import asyncio
import signal
import importlib
from contextlib import suppress

from anony import (anon, app, config, db, logger,
                   stop, thumb, userbot, yt)
from anony.plugins import all_modules


def setup_signal_handlers(stop_event: asyncio.Event):
    loop = asyncio.get_running_loop()
    received_signal = None
    registered_handlers = []
    previous_handlers = {}

    def request_shutdown(signum):
        nonlocal received_signal

        if received_signal is None:
            received_signal = signal.Signals(signum).name
            logger.info("Received %s. Shutting down...", received_signal)
        stop_event.set()

    def signal_handler(signum, _frame):
        loop.call_soon_threadsafe(request_shutdown, signum)

    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGABRT):
        try:
            loop.add_signal_handler(sig, request_shutdown, sig)
            registered_handlers.append(sig)
        except NotImplementedError:
            with suppress(ValueError):
                previous_handlers[sig] = signal.getsignal(sig)
                signal.signal(sig, signal_handler)
        except (RuntimeError, ValueError):
            pass

    def cleanup():
        for sig in registered_handlers:
            with suppress(NotImplementedError, RuntimeError, ValueError):
                loop.remove_signal_handler(sig)
        for sig, previous in previous_handlers.items():
            with suppress(ValueError):
                signal.signal(sig, previous)

    return cleanup


async def idle(stop_event: asyncio.Event):
    await stop_event.wait()


async def main():
    started = False
    stop_event = asyncio.Event()
    cleanup_signal_handlers = setup_signal_handlers(stop_event)
    try:
        await db.connect()
        if stop_event.is_set():
            return
        await app.boot()
        if stop_event.is_set():
            return
        await userbot.boot()
        if stop_event.is_set():
            return
        await anon.boot()
        if stop_event.is_set():
            return
        await thumb.start()
        started = True
        if stop_event.is_set():
            return

        for module in all_modules:
            importlib.import_module(f"anony.plugins.{module}")
        logger.info(f"Loaded {len(all_modules)} modules.")
        if stop_event.is_set():
            return

        if config.COOKIES_URL:
            await yt.save_cookies(config.COOKIES_URL)
            if stop_event.is_set():
                return

        sudoers = await db.get_sudoers()
        app.sudoers.update(sudoers)
        app.bl_users.update(await db.get_blacklisted())
        logger.info(f"Loaded {len(app.sudoers)} sudo users.")

        await idle(stop_event)
    finally:
        try:
            # Await shutdown so cleanup completes before asyncio.run closes the loop.
            await stop(ignore_cleanup_errors=not started)
        finally:
            cleanup_signal_handlers()


if __name__ == "__main__":
    try:
        # asyncio.run is the modern entry point and manages loop lifecycle cleanup.
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
