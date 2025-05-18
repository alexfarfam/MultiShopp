import mitt from 'mitt';

const emitter = mitt();

export const sendEvent = emitter.emit
export const useListen = emitter.on