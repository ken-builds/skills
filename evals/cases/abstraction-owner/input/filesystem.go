package reports

import "os"

type FileStore struct{}
func (FileStore) Save(name string, data []byte) error {
    return os.WriteFile(name, data, 0600)
}
