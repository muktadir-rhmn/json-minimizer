const PRIMITIVE = 0

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
        } else if (type === "object") {
            return this.#restoreObject(schema, data);
        } else{
            return data;
        }
    }

    #restoreObject(schema, data) {
        const fields = Object.keys(data).slice().sort(); // creates a copy before sorting. otherwise, sorting will mutate key order

        const restoredData = {};
        let i = 0;
        for (const field of fields) {
            restoredData[field] = this.#restore(schema[field], data[i]);

            i++;
        }
        return restoredData;
    }

}