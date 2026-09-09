package reports

type Store interface { Save(name string, data []byte) error }

func Publish(store Store, name string, data []byte) error {
    return store.Save(name, data)
}
