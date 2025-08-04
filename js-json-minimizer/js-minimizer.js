const PRIMITIVE = 0;

class JSONMinimizer {
    minimize(data) {
        if (data == null) {
            return data;
        }
        const type = typeof data;
        if (type === "function") {
            throw "Invalid: Functions cannot be restored.";
        } else if (type === "object") {
            return this.#minimizeObject(data);
        } else if (Array.isArray(data)) {
            return this.#minimizeArray(data);
        } else {
            return data;
        }
    }

    #minimizeObject(data) {
        const fields = Object.keys(data).slice().sort(); // creates a copy before sorting. otherwise, sorting will mutate key order

        const minimizedData = [];
        for (const field of fields) {
            const minimizedFieldData = this.minimize(data[field]);
            minimizedData.push(minimizedFieldData);
        }
        return minimizedData;
    }

    #minimizeArray(data) {
        const minimizedData = [];
        for (const item of data) {
            const minimizedItem = this.minimize(item);
            minimizedData.push(minimizedItem);
        }
        return minimizedData;
    }
}

class JSONRestorer {
     constructor(schema) {
        this.schema = schema;
    }

    restore(data) {
        if (data == null) {
            return data;
        }
        return this.#restore(this.schema, data)
    }

    #restore(schema, data) {
        const type = typeof schema;
        if (type === "function") {
            throw "Invalid Schema: Functions cannot be restored.";
        } else if (Array.isArray(schema)) {
            return this.#restoreArray(schema, data);
        } else if (type === "object") {
            return this.#restoreObject(schema, data);
        } else {
            return data;
        }
    }

    #restoreObject(schema, data) {
        if (typeof schema !== "object") {
            throw "Schema is supposed to be an object";
        }

        if (!Array.isArray(data)) {
            throw "Data is supposed to be an object";
        }

        const fields = Object.keys(schema).slice().sort(); // creates a copy before sorting. otherwise, sorting will mutate key order

        const restoredData = {};
        let i = 0;
        for (const field of fields) {
            restoredData[field] = this.#restore(schema[field], data[i]);
            i++;
        }
        return restoredData;
    }

    #restoreArray(schema, data) {
        if (!Array.isArray(schema)) {
            throw "Schema is supposed to be an array";
        }
        if (!Array.isArray(data)) {
            throw "Data is supposed to an array";
        }
        if (schema.length != 1) {
            throw "List schema is supposed to have exactly one element";
        }

        const itemSchema = schema[0];
        const restoredArray = [];
        for (const item of data) {
            const restoredItem = this.#restore(itemSchema, item);
            restoredArray.push(restoredItem);
        }
        return restoredArray;
    }

}